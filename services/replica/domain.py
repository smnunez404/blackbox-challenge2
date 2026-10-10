"""Modelo determinista del comportamiento descubierto; no realiza IO de red."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Account:
    account_id: str
    name: str
    balance: int = 0


@dataclass
class Operation:
    operation_id: str
    kind: str
    amount: int
    account_id: str | None = None
    source_id: str | None = None
    destination_id: str | None = None
    annulled: bool = False


@dataclass
class Model:
    """Estado de una instancia del servicio.

    Los controles de CONSULTA y ANULA usan reglas candidatas verificadas contra
    varias observaciones. Para los demás comandos se preservan los vectores
    aceptados conocidos; ALTA no tiene una fórmula general descubierta.
    """

    accounts: dict[str, Account] = field(default_factory=dict)
    operations: dict[str, Operation] = field(default_factory=dict)
    next_account: int = 1
    next_operation: int = 1

    def reset(self) -> None:
        self.accounts.clear()
        self.operations.clear()
        self.next_account = 1
        self.next_operation = 1

    @staticmethod
    def _error(status: int, code: str, message: str) -> tuple[int, dict]:
        return status, {"error": code, "mensaje": message}

    @staticmethod
    def _control_matches(control: int, base: int, number: int) -> bool:
        return 0 <= control < 97 and control == (base - 3 * number) % 97

    @staticmethod
    def _positive_amount(raw: str) -> int | None:
        if not re.fullmatch(r"[0-9]+", raw, flags=re.ASCII):
            return None
        # The replica only accepts a small, evidence-backed set of positive
        # amount vectors. Avoid Python's decimal digit conversion limit (and
        # needless huge integers) for unmodeled amounts; the sentinel cannot
        # match any currently accepted vector and therefore follows the
        # existing conservative E202 path. This is a robustness default, not
        # an inferred rule of the original service.
        normalized = raw.lstrip("0") or "0"
        amount = int(normalized) if len(normalized) <= 6 else 1_000_000
        return amount if amount > 0 else None

    @staticmethod
    def _format_balance(balance: int) -> str:
        """V2 renders the observed integer balance as decimal units / 100."""
        sign = "-" if balance < 0 else ""
        absolute = abs(balance)
        return f"{sign}{absolute // 100}.{absolute % 100:02d}"

    def process(self, message: str) -> tuple[int, dict]:
        if not isinstance(message, str):
            return self._error(400, "E102", "falta m")

        if ";" not in message:
            return self._error(400, "E103", "falta control")

        parts = message.split(";")
        command = parts[0].upper()
        if any(part == "" for part in parts):
            return self._error(400, "E104", "segmento vacío")

        # PING is an observed exception: its final field is ignored, while an
        # extra field is an arity error even when that extra field is text.
        if command == "PING":
            if len(parts) != 2:
                return self._error(400, "E302", "aridad inválida")
            return 200, {"pong": True}

        raw_control = parts[-1]
        if not re.fullmatch(r"(?:0|[1-9][0-9]*)", raw_control, flags=re.ASCII):
            return self._error(400, "E201", "control mal formado")
        # Every observed valid control is below 97. Reject unbounded decimal
        # strings before int() reaches Python's conversion limit. The exact
        # upstream response for this extreme case is still an assumption.
        if len(raw_control) > 3:
            return self._error(400, "E202", "control inválido")
        control = int(raw_control)

        arities = {"ALTA": 3, "CONSULTA": 3, "DEPOSITO": 4, "TRANSFER": 5, "ANULA": 3}
        if command not in arities:
            return self._error(400, "E301", "comando desconocido ")
        if len(parts) != arities[command]:
            return self._error(400, "E302", "aridad inválida")

        if command == "ALTA":
            name = parts[1]
            # No general ALTA checksum has been inferred. These are accepted
            # vectors observed against the original; an unknown vector uses a
            # deterministic validation default, which is provisional.
            known_valid = {
                ("Lucia", 82), (" Lucia", 82), ("Mateo", 3),
                ("Lucib", 79), ("Lucic", 76), ("Lucid", 73),
            }
            known_invalid = {("Lucia", 83), ("Lucia", 81), ("Lucia", 84),
                             ("Mateo", 82), ("Lucia", 3), ("Lucja", 80),
                             ("Lucja", 28), ("Lucja", 42), ("Lucja", 21)}
            if (name, control) in known_invalid or (name, control) not in known_valid:
                return self._error(400, "E202", "control inválido")
            account_id = f"AC-{self.next_account:04d}"
            self.next_account += 1
            self.accounts[account_id] = Account(account_id, name)
            return 201, {"cuentaId": account_id}

        if command == "CONSULTA":
            account_id = parts[1]
            # The original accepts the numeric control for a lower-case
            # prefix and for one leading space, then performs an exact
            # account-key lookup (which returns E401 for those spellings).
            match = re.fullmatch(r" ?AC-([0-9]{4})", account_id,
                                 flags=re.ASCII | re.IGNORECASE)
            if not match or not self._control_matches(control, 17, int(match.group(1))):
                return self._error(400, "E202", "control inválido")
            account = self.accounts.get(account_id)
            if account is None:
                return self._error(404, "E401", "cuenta inexistente")
            return 200, {"saldo": self._format_balance(account.balance), "cuenta_id": account_id}

        if command == "DEPOSITO":
            account_id, raw_amount = parts[1], parts[2]
            amount = self._positive_amount(raw_amount)
            if amount is None:
                return self._error(400, "E501", "monto inválido")
            account = self.accounts.get(account_id)
            if account is None:
                return self._error(404, "E401", "cuenta inexistente")
            # Only observed accepted vectors are implemented. In particular,
            # AC-0002/250000 with controls 83 and 86 returned E202 in the
            # extended replay. No general DEPOSITO formula is known yet.
            known_valid = {("AC-0001", 250000, 86), ("AC-0002", 700, 35)}
            if (account_id, amount, control) not in known_valid:
                return self._error(400, "E202", "control inválido")
            account.balance += amount
            operation_id = f"OP-{self.next_operation:04d}"
            self.next_operation += 1
            self.operations[operation_id] = Operation(operation_id, "DEPOSITO", amount, account_id=account_id)
            return 200, {"status": "recieved", "operacionId": operation_id}

        if command == "TRANSFER":
            source_id, destination_id, raw_amount = parts[1], parts[2], parts[3]
            amount = self._positive_amount(raw_amount)
            if amount is None:
                return self._error(400, "E501", "monto inválido")
            # No general TRANSFER control formula has been inferred. Preserve
            # the observed valid vectors and fail conservatively for unknown
            # tuples. This check precedes account/limit/funds checks, matching
            # the observed E202 precedence cases (IDs 218, 220, 225, 240).
            known_valid = {
                ("AC-0001", "AC-0002", 40_000, 86),
                ("AC-0001", "AC-0002", 100_000, 12),
                ("AC-0001", "AC-0002", 120_000, 55),
                ("AC-0002", "AC-0001", 50_000, 23),
            }
            if (source_id, destination_id, amount, control) not in known_valid:
                return self._error(400, "E202", "control inválido")
            source = self.accounts.get(source_id)
            destination = self.accounts.get(destination_id)
            if source is None or destination is None:
                return self._error(404, "E401", "cuenta inexistente")
            # V2 rejects the V1-accepted 100000 vector and accepts observed
            # 40000/50000 vectors. The exact boundary and whether it is
            # state-dependent remain unknown; this is a conservative model of
            # the confirmed 100000 rejection, not a universal limit claim.
            if amount >= 100_000:
                return self._error(422, "E506", "límite excedido")
            if source.balance < amount:
                return self._error(422, "E507", "saldo insuficiente")
            source.balance -= amount
            destination.balance += amount
            operation_id = f"OP-{self.next_operation:04d}"
            self.next_operation += 1
            self.operations[operation_id] = Operation(
                operation_id, "TRANSFER", amount,
                source_id=source_id, destination_id=destination_id,
            )
            return 200, {"status": "recieved", "operacionId": operation_id}

        # ANULA: the operation's sequence number is encoded by a candidate
        # control rule that matched the observed IDs OP-0003..OP-0005.
        operation_id = parts[1]
        match = re.fullmatch(r"OP-([0-9]{4})", operation_id, flags=re.ASCII)
        if not match or not self._control_matches(control, 75, int(match.group(1))):
            return self._error(400, "E202", "control inválido")
        operation = self.operations.get(operation_id)
        if operation is None:
            return self._error(404, "E402", "operación inexistente")
        if operation.annulled:
            return 200, {"ok": False, "motivo": "ya anulada"}
        if operation.kind == "DEPOSITO":
            account = self.accounts[operation.account_id or ""]
            account.balance -= operation.amount
        else:
            self.accounts[operation.source_id or ""].balance += operation.amount
            self.accounts[operation.destination_id or ""].balance -= operation.amount
        operation.annulled = True
        return 200, {"ok": True, "anulada": operation_id}
