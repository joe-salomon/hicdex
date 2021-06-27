from dipdup.models import OperationData, Transaction, Origination, BigMapDiff, BigMapData, BigMapAction
from dipdup.context import HandlerContext, RollbackHandlerContext
from typing import Optional


import hicdex.models as models

from hicdex.types.objktbid_english.parameter.bid import BidParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_bid_english(
    ctx: HandlerContext,
    bid: Transaction[BidParameter, ObjktbidEnglishStorage],
) -> None:
    auction = await models.EnglishAuction.filter(id=int(bid.parameter.__root__)).get()
    bidder, _ = await models.Holder.get_or_create(address=bid.data.sender_address)

    bid = models.EnglishBid(
        bidder=bidder,
        amount=bid.data.amount,
        auction=auction,

        timestamp=bid.data.timestamp,
        level=bid.data.level,
    )
    await bid.save()
