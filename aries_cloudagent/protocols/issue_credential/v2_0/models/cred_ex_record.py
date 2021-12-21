"""Aries#0453 v2.0 credential exchange information with non-secrets storage."""

import logging

from typing import Any, Mapping, Union

from marshmallow import fields, Schema, validate

from .....core.profile import ProfileSession
from .....messaging.models.base_record import BaseExchangeRecord, BaseExchangeSchema
from .....messaging.valid import UUIDFour
from .....storage.base import StorageError

from ..messages.cred_format import V20CredFormat
from ..messages.cred_issue import V20CredIssue, V20CredIssueSchema
from ..messages.cred_proposal import V20CredProposal, V20CredProposalSchema
from ..messages.cred_offer import V20CredOffer, V20CredOfferSchema
from ..messages.cred_request import V20CredRequest, V20CredRequestSchema
from ..messages.inner.cred_preview import V20CredPreviewSchema

from . import UNENCRYPTED_TAGS

LOGGER = logging.getLogger(__name__)


class V20CredExRecord(BaseExchangeRecord):
    """Represents an Aries#0036 credential exchange."""

    class Meta:
        """CredentialExchange metadata."""

        schema_class = "V20CredExRecordSchema"

    RECORD_TYPE = "cred_ex_v20"
    RECORD_ID_NAME = "cred_ex_id"
    RECORD_TOPIC = "issue_credential_v2_0"
    TAG_NAMES = {
        "~thread_id" if UNENCRYPTED_TAGS else "thread_id",
        "revoc_reg_id",
        "revocation_id",
    }

    INITIATOR_SELF = "self"
    INITIATOR_EXTERNAL = "external"
    ROLE_ISSUER = "issuer"
    ROLE_HOLDER = "holder"

    STATE_PROPOSAL_SENT = "proposal-sent"
    STATE_PROPOSAL_RECEIVED = "proposal-received"
    STATE_OFFER_SENT = "offer-sent"
    STATE_OFFER_RECEIVED = "offer-received"
    STATE_REQUEST_SENT = "request-sent"
    STATE_REQUEST_RECEIVED = "request-received"
    STATE_ISSUED = "credential-issued"
    STATE_CREDENTIAL_RECEIVED = "credential-received"
    STATE_DONE = "done"
    STATE_CREDENTIAL_REVOKED = "credential-revoked"

    def __init__(
        self,
        *,
        cred_ex_id: str = None,
        connection_id: str = None,
        thread_id: str = None,
        parent_thread_id: str = None,
        initiator: str = None,
        role: str = None,
        state: str = None,
        cred_proposal: Union[Mapping, V20CredProposal] = None,  # aries message
        cred_offer: Union[Mapping, V20CredOffer] = None,  # aries message
        cred_request: Union[Mapping, V20CredRequest] = None,  # aries message
        cred_issue: Union[Mapping, V20CredIssue] = None,  # aries message
        auto_offer: bool = False,
        auto_issue: bool = False,
        auto_remove: bool = True,
        error_msg: str = None,
        trace: bool = False,  # backward compat: BaseRecord.from_storage()
        cred_id_stored: str = None,  # backward compat: BaseRecord.from_storage()
        conn_id: str = None,  # backward compat: BaseRecord.from_storage()
        by_format: Mapping = None,  # backward compat: BaseRecord.from_storage()
        revoc_reg_id: str = None,  # ignore
        revocation_id: str = None,  # ignore
        **kwargs,
    ):
        """Initialize a new V20CredExRecord."""
        super().__init__(cred_ex_id, state, trace=trace, **kwargs)
        self._id = cred_ex_id
        self.connection_id = connection_id or conn_id
        self.thread_id = thread_id
        self.parent_thread_id = parent_thread_id
        self.initiator = initiator
        self.role = role
        self.state = state
        self._cred_proposal = V20CredProposal.serde(cred_proposal)
        self._cred_offer = V20CredOffer.serde(cred_offer)
        self._cred_request = V20CredRequest.serde(cred_request)
        self._cred_issue = V20CredIssue.serde(cred_issue)
        self.auto_offer = auto_offer
        self.auto_issue = auto_issue
        self.auto_remove = auto_remove
        self.error_msg = error_msg

    @property
    def cred_ex_id(self) -> str:
        """Accessor for the ID associated with this exchange."""
        return self._id

    @property
    def cred_preview(self) -> Mapping:
        """Credential preview (deserialized view) from credential proposal."""
        return self.cred_proposal and self.cred_proposal.credential_preview or None

    @property
    def cred_proposal(self) -> V20CredProposal:
        """Accessor; get deserialized view."""
        return None if self._cred_proposal is None else self._cred_proposal.de

    @property
    def revoc_reg_id(self) -> str:
        """Accessor; get revoc_reg_id if available."""
        cred_issue_data = None if self._cred_issue is None else self._cred_issue.de
        print("cred_issue_data:", cred_issue_data)
        # TODO need to decode cred_issue_data to see if it contains revoc_reg_id
        return None if cred_issue_data is None else "tester_revoc_reg_id"

    @property
    def revocation_id(self) -> str:
        """Accessor; get revocation_id if available."""
        cred_issue_data = None if self._cred_issue is None else self._cred_issue.de
        print("cred_issue_data:", cred_issue_data)
        # TODO need to decode cred_issue_data to see if it contains revocation_id
        return None if cred_issue_data is None else "tester_revocation_id"

    @cred_proposal.setter
    def cred_proposal(self, value):
        """Setter; store de/serialized views."""
        self._cred_proposal = V20CredProposal.serde(value)

    @property
    def cred_offer(self) -> V20CredOffer:
        """Accessor; get deserialized view."""
        return None if self._cred_offer is None else self._cred_offer.de

    @cred_offer.setter
    def cred_offer(self, value):
        """Setter; store de/serialized views."""
        self._cred_offer = V20CredOffer.serde(value)

    @property
    def cred_request(self) -> V20CredRequest:
        """Accessor; get deserialized view."""
        return None if self._cred_request is None else self._cred_request.de

    @cred_request.setter
    def cred_request(self, value):
        """Setter; store de/serialized views."""
        self._cred_request = V20CredRequest.serde(value)

    @property
    def cred_issue(self) -> V20CredIssue:
        """Accessor; get deserialized view."""
        return None if self._cred_issue is None else self._cred_issue.de

    @cred_issue.setter
    def cred_issue(self, value):
        """Setter; store de/serialized views."""
        self._cred_issue = V20CredIssue.serde(value)

    async def save_error_state(
        self,
        session: ProfileSession,
        *,
        reason: str = None,
        log_params: Mapping[str, Any] = None,
        log_override: bool = False,
    ):
        """
        Save record error state if need be; log and swallow any storage error.

        Args:
            session: The profile session to use
            reason: A reason to add to the log
            log_params: Additional parameters to log
            override: Override configured logging regimen, print to stderr instead
        """

        if self._last_state is None:  # already done
            return

        self.state = None
        if reason:
            self.error_msg = reason

        try:
            await self.save(
                session,
                reason=reason,
                log_params=log_params,
                log_override=log_override,
            )
        except StorageError as err:
            LOGGER.exception(err)

    @property
    def record_value(self) -> Mapping:
        """Accessor for the JSON record value generated for this credential exchange."""
        return {
            **{
                prop: getattr(self, prop)
                for prop in (
                    "connection_id",
                    "parent_thread_id",
                    "initiator",
                    "role",
                    "state",
                    "auto_offer",
                    "auto_issue",
                    "auto_remove",
                    "error_msg",
                    "trace",
                )
            },
            **{
                prop: getattr(self, f"_{prop}").ser
                for prop in (
                    "cred_proposal",
                    "cred_offer",
                    "cred_request",
                    "cred_issue",
                )
                if getattr(self, prop) is not None
            },
        }

    @classmethod
    async def retrieve_by_conn_and_thread(
        cls, session: ProfileSession, connection_id: str, thread_id: str
    ) -> "V20CredExRecord":
        """Retrieve a credential exchange record by connection and thread ID."""
        cache_key = f"credential_exchange_ctidx::{connection_id}::{thread_id}"
        record_id = await cls.get_cached_key(session, cache_key)
        if record_id:
            record = await cls.retrieve_by_id(session, record_id)
        else:
            record = await cls.retrieve_by_tag_filter(
                session,
                {"thread_id": thread_id},
                {"connection_id": connection_id} if connection_id else None,
            )
            await cls.set_cached_key(session, cache_key, record.cred_ex_id)
        return record

    @property
    def by_format(self) -> Mapping:
        """Record proposal, offer, request, and credential attachments by format."""
        result = {}
        for item, cls in {
            "cred_proposal": V20CredProposal,
            "cred_offer": V20CredOffer,
            "cred_request": V20CredRequest,
            "cred_issue": V20CredIssue,
        }.items():
            msg = getattr(self, item)
            if msg:
                result.update(
                    {
                        item: {
                            V20CredFormat.Format.get(f.format).api: msg.attachment(
                                V20CredFormat.Format.get(f.format)
                            )
                            for f in msg.formats
                        }
                    }
                )

        return result

    def __eq__(self, other: Any) -> bool:
        """Comparison between records."""
        return super().__eq__(other)


class V20CredExRecordSchema(BaseExchangeSchema):
    """Schema to allow serialization/deserialization of credential exchange records."""

    class Meta:
        """V20CredExSchema metadata."""

        model_class = V20CredExRecord

    cred_ex_id = fields.Str(
        required=False,
        description="Credential exchange identifier",
        example=UUIDFour.EXAMPLE,
    )
    connection_id = fields.Str(
        required=False, description="Connection identifier", example=UUIDFour.EXAMPLE
    )
    thread_id = fields.Str(
        required=False, description="Thread identifier", example=UUIDFour.EXAMPLE
    )
    parent_thread_id = fields.Str(
        required=False, description="Parent thread identifier", example=UUIDFour.EXAMPLE
    )
    initiator = fields.Str(
        required=False,
        description="Issue-credential exchange initiator: self or external",
        example=V20CredExRecord.INITIATOR_SELF,
        validate=validate.OneOf(
            [
                getattr(V20CredExRecord, m)
                for m in vars(V20CredExRecord)
                if m.startswith("INITIATOR_")
            ]
        ),
    )
    role = fields.Str(
        required=False,
        description="Issue-credential exchange role: holder or issuer",
        example=V20CredExRecord.ROLE_ISSUER,
        validate=validate.OneOf(
            [
                getattr(V20CredExRecord, m)
                for m in vars(V20CredExRecord)
                if m.startswith("ROLE_")
            ]
        ),
    )
    state = fields.Str(
        required=False,
        description="Issue-credential exchange state",
        example=V20CredExRecord.STATE_DONE,
        validate=validate.OneOf(
            [
                getattr(V20CredExRecord, m)
                for m in vars(V20CredExRecord)
                if m.startswith("STATE_")
            ]
        ),
    )
    cred_preview = fields.Nested(
        V20CredPreviewSchema(),
        required=False,
        dump_only=True,
        description="Credential preview from credential proposal",
    )
    cred_proposal = fields.Nested(
        V20CredProposalSchema(),
        required=False,
        description="Credential proposal message",
    )
    cred_offer = fields.Nested(
        V20CredOfferSchema(),
        required=False,
        description="Credential offer message",
    )
    cred_request = fields.Nested(
        V20CredRequestSchema(),
        required=False,
        description="Serialized credential request message",
    )
    cred_issue = fields.Nested(
        V20CredIssueSchema(),
        required=False,
        description="Serialized credential issue message",
    )
    by_format = fields.Nested(
        Schema.from_dict(
            {
                "cred_proposal": fields.Dict(required=False),
                "cred_offer": fields.Dict(required=False),
                "cred_request": fields.Dict(required=False),
                "cred_issue": fields.Dict(required=False),
            },
            name="V20CredExRecordByFormatSchema",
        ),
        required=False,
        description=(
            "Attachment content by format for proposal, offer, request, and issue"
        ),
        dump_only=True,
    )
    auto_offer = fields.Bool(
        required=False,
        description="Holder choice to accept offer in this credential exchange",
        example=False,
    )
    auto_issue = fields.Bool(
        required=False,
        description="Issuer choice to issue to request in this credential exchange",
        example=False,
    )
    auto_remove = fields.Bool(
        required=False,
        default=True,
        description=(
            "Issuer choice to remove this credential exchange record when complete"
        ),
        example=False,
    )
    error_msg = fields.Str(
        required=False,
        description="Error message",
        example="The front fell off",
    )
