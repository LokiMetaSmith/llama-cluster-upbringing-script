import pytest
from pipecatapp.tools.personality_tool import PersonalityTool
from pipecatapp.tools.p2p_sync_tool import P2PSyncTool
from pipecatapp.tools.vr_tool import VRTool

def test_personaplex_voice_persona():
    tool = PersonalityTool()

    res = tool.set_voice_persona(voice_id="NATF2", role_prompt="Mission Controller", emotion="authoritative")
    assert "NATF2" in res
    assert "authoritative" in res

    err_res = tool.set_voice_persona(voice_id="INVALID_VOICE", role_prompt="Test")
    assert "Error: Voice ID 'INVALID_VOICE' not supported" in err_res

def test_p2p_prompt_cache_route(tmp_path):
    sync_tool = P2PSyncTool(base_dir=str(tmp_path))
    res = sync_tool.run("p2p_prompt_cache_route", prompt_hash="hash_abc123", transport="hyperswarm")
    assert "Routed prompt cache hash_abc123" in res
    assert "hyperswarm" in res

@pytest.mark.asyncio
async def test_vr_tool_broadcasts():
    vr = VRTool()
    res_persona = await vr.broadcast_persona_emotion("agent_1", "NATF2", "authoritative")
    assert "authoritative" in res_persona

    res_p2p = await vr.broadcast_p2p_telemetry("node_a", "node_b", 45.2, "ble")
    assert "45.2 Mbps" in res_p2p
    assert "ble" in res_p2p
