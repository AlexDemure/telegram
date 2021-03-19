import plotly.graph_objects as go


def generate_burndown_chart(tasks):
    pass

# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# x = [str(y) for y in x]
# fig = go.Figure()
#
# fig.add_trace(go.Scatter(
#     x=x,
#     y=[16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
#     name='<b>No</b> Gaps',  # Style name/legend entry with html tags
#     # connectgaps=True  # override default to connect the gaps
#     mode="lines+markers",
# ))
# fig.add_trace(go.Scatter(
#     x=x,
#     y=[15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
#     name='Gaps',
#     mode="lines+markers",
# ))
#
# # fig.update_xaxes(
# #     autorange=False,
# #     range=[0, len(x)]
# # )
#
#
#
# import tempfile
# from aiogram.types import InputFile
# with tempfile.NamedTemporaryFile(suffix=f'.jpg') as file:
#     fig.write_image(file.name)
#     await bot.send_document(message.chat.id, InputFile(file.name))