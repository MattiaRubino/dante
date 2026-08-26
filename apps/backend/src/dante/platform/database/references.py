"""Typed UUID reference families and explicit UUIDv7 issuance for DANTE persistence."""

from typing import NewType
from uuid import UUID, uuid7

NativeRef = NewType("NativeRef", UUID)
ScopedRecordRef = NewType("ScopedRecordRef", UUID)
MaterialStateRef = NewType("MaterialStateRef", UUID)


def new_native_ref() -> NativeRef:
    """Issue one application-owned UUIDv7 NativeRef."""
    return NativeRef(uuid7())


def new_scoped_record_ref() -> ScopedRecordRef:
    """Issue one application-owned UUIDv7 ScopedRecordRef."""
    return ScopedRecordRef(uuid7())


def new_material_state_ref() -> MaterialStateRef:
    """Issue one application-owned UUIDv7 MaterialStateRef."""
    return MaterialStateRef(uuid7())
