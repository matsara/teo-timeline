from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


# =========================================================
# 2. FUNÇÕES DE SUPORTE
# =========================================================
def gerar_html_final(alertas_selecionados):
    html_rows = ""
    for i, alerta in enumerate(alertas_selecionados):
        classe = "linha-clara" if i % 2 == 0 else "linha-escura"
        acionamentos = alerta["acionamentos"] if alerta["acionamentos"] else [{
            "nome": "-", "time": "-", "horario": "-", "atendeu": "-", "status_acionamento": "-"
        }]

        primeira = acionamentos[0]
        restantes = acionamentos[1:]
        rowspan = len(acionamentos)

        html_rows += f"""
        <tr class="{classe}">
            <td rowspan="{rowspan}">{alerta['ticket']}</td>
            <td rowspan="{rowspan}">{alerta['evento']}</td>
            <td rowspan="{rowspan}">{alerta.get('status_atual', 'Sem acionamento')}</td>
            <td>{primeira.get('nome', '-')}</td>
            <td>{primeira.get('time', '-')}</td>
            <td>{primeira.get('horario', '-')}</td>
            <td>{primeira.get('status_acionamento', '-')}</td>
            <td>{primeira.get('atendeu', '-')}</td>
        </tr>"""

        for a in restantes:
            html_rows += f"""
            <tr class="{classe}">
                <td>{a.get('nome', '-')}</td>
                <td>{a.get('time', '-')}</td>
                <td>{a.get('horario', '-')}</td>
                <td>{a.get('status_acionamento', '-')}</td>
                <td>{a.get('atendeu', '-')}</td>
            </tr>"""

    descricoes = []
    for alerta in alertas_selecionados:
        descricao = (alerta.get("descricao_timeline") or "").strip()
        if descricao:
            descricoes.append(f"<li><b>{alerta['ticket']}</b>: {descricao}</li>")

    bloco_descricao = ""
    if descricoes:
        bloco_descricao = (
            "<div class='descricao-wrap'><h3>Analista DOC</h3><ul>"
            + "".join(descricoes)
            + "</ul></div>"
        )

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 0; padding: 0; }}
            th, td {{ border: 1px solid #000; padding: 8px; text-align: center; vertical-align: middle; font-size: 13px; }}
            th {{ background-color: #ff4d1a; color: white; font-weight: bold; }}
            .titulo {{ 
                background-color: #0b1f4d; color: white; font-size: 18px; 
                font-weight: bold; text-align: center; padding: 12px;
                border: 1px solid #000; border-bottom: none;
                margin-bottom: 0;
            }}
            .linha-clara {{ background-color: #ffffff; }}
            .linha-escura {{ background-color: #f7f7f7; }}
            .descricao-wrap {{
                border: 1px solid #c8d7ff;
                background: #f5f8ff;
                padding: 12px 16px;
                margin: 0 0 12px 0;
            }}
            .descricao-wrap h3 {{ margin: 0 0 8px 0; color: #0b1f4d; font-size: 15px; }}
            .descricao-wrap ul {{ margin: 0; padding-left: 18px; }}
            .descricao-wrap li {{ margin: 4px 0; font-size: 13px; }}
        </style>
    </head>
    <body>
        {bloco_descricao}
        <div class="titulo">Timeline de Acionamentos</div>
        <table>
            <thead>
                <tr>
                    <th rowspan="2">Ticket</th>
                    <th rowspan="2">Evento</th>
                    <th rowspan="2">Status Atual</th>
                    <th colspan="5">Acionamentos</th>
                </tr>
                <tr>
                    <th>Nome Completo</th>
                    <th>Time</th>
                    <th>Horário</th>
                    <th>Status Acionamento</th>
                    <th>Atendeu?</th>
                </tr>
            </thead>
            <tbody>{html_rows}</tbody>
        </table>
    </body>
    </html>
    """


def gerar_resumo_texto(alertas_selecionados):
    resumo_txt = "TEO - RESUMO DE ALERTAS\n" + "=" * 40 + "\n\n"

    for alerta in alertas_selecionados:
        resumo_txt += f"ANALISTA DOC: {(alerta.get('descricao_timeline') or '-')}\n"
        resumo_txt += (
            f"TICKET: {alerta['ticket']}\n"
            f"EVENTO: {alerta['evento']}\n"
            f"STATUS ATUAL: {alerta.get('status_atual', 'Sem acionamento')}\n"
        )

        resumo_txt += "ESCALONAMENTO:\n"
        if alerta["acionamentos"]:
            for ac in alerta["acionamentos"]:
                resumo_txt += (
                    f"  - {ac['horario']} | {ac['nome']} ({ac['time']})"
                    f" | Status: {ac.get('status_acionamento', '-')}"
                    f" | Atendeu: {ac['atendeu']}\n"
                )
        else:
            resumo_txt += "  - Sem acionamentos\n"

        resumo_txt += "--------------------\n\n"

    return resumo_txt


def gerar_imagem_resumo_png(alertas_selecionados):
    resumo = gerar_resumo_texto(alertas_selecionados)
    linhas = resumo.splitlines()

    fonte = ImageFont.load_default()
    largura = 1400
    altura_linha = 22
    margem = 20
    altura = margem * 2 + max(1, len(linhas)) * altura_linha

    imagem = Image.new("RGB", (largura, altura), color=(19, 23, 34))
    draw = ImageDraw.Draw(imagem)

    y = margem
    for linha in linhas:
        draw.text((margem, y), linha, fill=(235, 239, 247), font=fonte)
        y += altura_linha

    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    return buffer.getvalue()


def gerar_imagem_timeline_png(alertas_selecionados):
    headers = ["Ticket", "Evento", "Status Atual"]
    acion_headers = ["Nome Completo", "Time", "Horario", "Status Acionamento", "Atendeu?"]
    col_widths = [140, 420, 320, 200, 90, 200, 430, 120]
    row_h = 40
    margin = 16

    grupos = []
    for alerta in alertas_selecionados:
        acionamentos = alerta.get("acionamentos") or [
            {
                "nome": "-",
                "time": "-",
                "horario": "-",
                "status_acionamento": "-",
                "atendeu": "-",
            }
        ]
        grupos.append((alerta, acionamentos))

    fonte = ImageFont.load_default()
    largura = margin * 2 + sum(col_widths)
    bloco_doc_h = 70
    titulo_h = 56
    header_h1 = 42
    header_h2 = 42
    total_linhas = sum(len(acionamentos) for _, acionamentos in grupos)
    altura_tabela = header_h1 + header_h2 + max(1, total_linhas) * row_h
    altura = margin * 2 + bloco_doc_h + titulo_h + altura_tabela

    img = Image.new("RGB", (largura, altura), color=(18, 22, 33))
    draw = ImageDraw.Draw(img)

    # Analista DOC
    doc_rect = (margin, margin, largura - margin, margin + bloco_doc_h)
    draw.rectangle(doc_rect, fill=(236, 239, 247), outline=(200, 210, 235), width=1)
    draw.text((margin + 14, margin + 10), "Analista DOC", fill=(20, 40, 90), font=fonte)
    doc_text = " | ".join(
        [f"{a.get('ticket', '-')}: {a.get('descricao_timeline', '-') or '-'}" for a in alertas_selecionados]
    )
    draw.text((margin + 14, margin + 34), doc_text, fill=(15, 18, 26), font=fonte)

    # Titulo
    y0 = margin + bloco_doc_h + 10
    draw.rectangle((margin, y0, largura - margin, y0 + titulo_h), fill=(24, 39, 90), outline=(24, 39, 90))
    draw.text((largura // 2 - 100, y0 + 18), "Timeline de Acionamentos", fill=(255, 255, 255), font=fonte)

    # Header principal (com agrupamento Acionamentos)
    y = y0 + titulo_h
    x = margin
    for i, h in enumerate(headers):
        w = col_widths[i]
        draw.rectangle((x, y, x + w, y + header_h1 + header_h2), fill=(255, 45, 12), outline=(0, 0, 0), width=1)
        draw.text((x + 8, y + 14), h, fill=(255, 255, 255), font=fonte)
        x += w

    # Header de Acionamentos
    ac_start_x = margin + sum(col_widths[:3])
    ac_total_w = sum(col_widths[3:])
    draw.rectangle(
        (ac_start_x, y, ac_start_x + ac_total_w, y + header_h1),
        fill=(255, 45, 12),
        outline=(0, 0, 0),
        width=1,
    )
    draw.text((ac_start_x + ac_total_w // 2 - 45, y + 14), "Acionamentos", fill=(255, 255, 255), font=fonte)

    x = ac_start_x
    for i, h in enumerate(acion_headers):
        w = col_widths[3 + i]
        draw.rectangle((x, y + header_h1, x + w, y + header_h1 + header_h2), fill=(255, 45, 12), outline=(0, 0, 0), width=1)
        draw.text((x + 8, y + header_h1 + 14), h, fill=(255, 255, 255), font=fonte)
        x += w

    # Linhas de dados com agrupamento por alerta (sem repetir ticket/evento/status)
    y += header_h1 + header_h2
    for gidx, (alerta, acionamentos) in enumerate(grupos):
        grupo_h = len(acionamentos) * row_h
        grupo_bg = (245, 245, 245) if gidx % 2 == 0 else (232, 232, 232)

        # Colunas com efeito de rowspan
        x = margin
        valores = [
            alerta.get("ticket", "-"),
            alerta.get("evento", "-"),
            alerta.get("status_atual", "Sem acionamento"),
        ]
        for i, valor in enumerate(valores):
            w = col_widths[i]
            draw.rectangle((x, y, x + w, y + grupo_h), fill=grupo_bg, outline=(0, 0, 0), width=1)
            draw.text((x + 8, y + grupo_h // 2 - 6), str(valor), fill=(20, 20, 20), font=fonte)
            x += w

        # Colunas de acionamentos (linha a linha)
        y_row = y
        for ridx, ac in enumerate(acionamentos):
            row_bg = grupo_bg if ridx % 2 == 0 else (224, 224, 224)
            x_row = margin + sum(col_widths[:3])
            dados = [
                ac.get("nome", "-"),
                ac.get("time", "-"),
                ac.get("horario", "-"),
                ac.get("status_acionamento", "-"),
                ac.get("atendeu", "-"),
            ]
            for i, cell in enumerate(dados):
                w = col_widths[3 + i]
                draw.rectangle((x_row, y_row, x_row + w, y_row + row_h), fill=row_bg, outline=(0, 0, 0), width=1)
                draw.text((x_row + 8, y_row + 12), str(cell), fill=(20, 20, 20), font=fonte)
                x_row += w
            y_row += row_h

        y += grupo_h

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
