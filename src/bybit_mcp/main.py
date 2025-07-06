import asyncio
import logging
import os

from dotenv import load_dotenv
from mcp.server import FastMCP

from .market import (
    get_funding_rate_history,
    get_index_price_kline,
    get_instruments_info,
    get_insurance,
    get_kline,
    get_long_short_ratio,
    get_mark_price_kline,
    get_open_interest,
    get_order_book,
    get_premium_index_price_kline,
    get_recent_trades,
    get_risk_limit,
    get_server_time,
    get_tickers,
)
from .position import (
    get_closed_pnl,
    get_position_info,
    modify_position_margin,
    set_auto_add_margin,
    set_leverage,
    set_trading_stop,
    switch_cross_isolated_margin,
    switch_position_mode,
)
from .trade import (
    amend_order,
    batch_amend_order,
    batch_cancel_order,
    batch_place_order,
    cancel_all_orders,
    cancel_order,
    get_account_info,
    get_open_closed_orders,
    get_order_history,
    get_single_coin_balance,
    get_trade_history,
    get_wallet_balance,
    place_order,
    place_trigger_order,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bybit-mcp")

port = int(os.getenv("MCP_PORT", "8000"))
server = FastMCP(name="bybit-mcp", host="0.0.0.0", port=port)

# Market data tools
server.add_tool(get_server_time)
server.add_tool(get_tickers)
server.add_tool(get_order_book)
server.add_tool(get_recent_trades)
server.add_tool(get_kline)
server.add_tool(get_mark_price_kline)
server.add_tool(get_index_price_kline)
server.add_tool(get_premium_index_price_kline)
server.add_tool(get_instruments_info)
server.add_tool(get_funding_rate_history)
server.add_tool(get_open_interest)
server.add_tool(get_insurance)
server.add_tool(get_risk_limit)
server.add_tool(get_long_short_ratio)

# Trading tools
server.add_tool(place_order)
server.add_tool(amend_order)
server.add_tool(cancel_order)
server.add_tool(get_open_closed_orders)
server.add_tool(cancel_all_orders)
server.add_tool(get_order_history)
server.add_tool(get_trade_history)
server.add_tool(batch_place_order)
server.add_tool(batch_amend_order)
server.add_tool(batch_cancel_order)
server.add_tool(get_wallet_balance)
server.add_tool(get_single_coin_balance)
server.add_tool(get_account_info)
server.add_tool(place_trigger_order)

# Position management
server.add_tool(get_position_info)
server.add_tool(get_closed_pnl)
server.add_tool(set_leverage)
server.add_tool(switch_cross_isolated_margin)
server.add_tool(switch_position_mode)
server.add_tool(set_trading_stop)
server.add_tool(set_auto_add_margin)
server.add_tool(modify_position_margin)

@server.resource("bybit://market/info", name="Bybit Market Information", mime_type="text/plain")
def market_info() -> str:
    return (
        "# Bybit MCP Server\n\n"
        "This MCP server provides access to Bybit's v5 Market API endpoints.\n\n"
        "## Available Endpoints:\n"
        "- get_server_time\n- get_tickers\n- get_order_book\n- get_recent_trades\n"
        "- get_kline\n- get_mark_price_kline\n- get_index_price_kline\n"
        "- get_premium_index_price_kline\n- get_instruments_info\n"
        "- get_funding_rate_history\n- get_open_interest\n- get_insurance\n"
        "- get_risk_limit\n- get_long_short_ratio\n"
    )

async def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    logger.info("Starting Bybit MCP Server in %s mode", transport)
    if transport == "stdio":
        await server.run_stdio_async()
    elif transport == "sse":
        await server.run_sse_async()
    else:
        raise ValueError(f"Unsupported MCP_TRANSPORT mode: {transport}")


def cli_main() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
