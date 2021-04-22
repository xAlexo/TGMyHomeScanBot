from pytest_mock import MockFixture

from commands.default import default
from contrib.ScanType import ScanType


async def test_default_all_correct(mocker: MockFixture):
    m: Mock = mocker.AsyncMock()
    m.pattern_match.groupdict = mocker.Mock(
        return_value={'ScanType': ScanType.Color, 'dpi': 300})
    m_msg = mocker.Mock(id=2)
    m_partial = mocker.Mock()
    m.chat_id = 1
    m.respond = mocker.AsyncMock(return_value=m_msg)

    p_scan = mocker.patch('commands.default.scan', mocker.AsyncMock())
    p_scan.return_value = 'tmp.png'

    p_partial = mocker.patch(
        'commands.default.partial', return_value=m_partial)
    p_progress = mocker.patch('commands.default.progress')

    await default(m)

    assert m.delete.called

    assert p_partial.called
    assert p_progress is p_partial.call_args_list[0].args[0]
    assert m is p_partial.call_args_list[0].args[1]
    assert m_msg is p_partial.call_args_list[0].args[2]

    assert p_scan.called
    assert 'Color' == p_scan.call_args_list[0].args[0]
    assert 300 == p_scan.call_args_list[0].args[1]
    assert m_partial is p_scan.call_args_list[0].args[2]

    assert m.respond.called
    assert 'Сканирую...' == m.respond.call_args_list[0].args[0]

    assert m.client.edit_message.called
    assert 1 == m.client.edit_message.call_args_list[0].args[0]
    assert m_msg is m.client.edit_message.call_args_list[0].args[1]
    assert 'Отправка' == m.client.edit_message.call_args_list[0].args[2]

    assert m.client.send_file.called
    mcsf_args = m.client.send_file.call_args_list[0]
    assert 'tmp.png' == mcsf_args[1]['file']
    assert mcsf_args[1]['force_document']
    assert 3 == len(mcsf_args[1]['buttons'])
    assert p_partial.return_value is mcsf_args[1]['progress_callback']

    assert m.client.delete_messages.called
    assert 1 == m.client.delete_messages.call_args_list[0].args[0]
    assert m_msg is m.client.delete_messages.call_args_list[0].args[1]


