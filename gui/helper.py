from paascrape.container import Answer

def _generate_paragraph(qna: Answer):
    html = f"""
    <article>
    <h2>{qna.question}</h2>
    """
    heading = f"<h4>{qna.answer_heading}</h4>" if qna.answer_heading else ''
    para = f"""
    <p>{qna.answer}</p>
    </article>
    """
    return html + heading + para

def _generate_table(qna: Answer):
    html = f"""
    <article>
    <h2>{qna.question}</h2>
    """
    heading = f"<h4>{qna.answer_heading}</h4>"
    table = "<table>"
    for i, lis in enumerate(qna.answer):
        tr = "<tr>"
        if i == 0:
            tr += ''.join([f'<th>{x}</th>' for x in lis])
        else:
            tr += ''.join([f'<td>{x}</td>' for x in lis])
            tr += "</tr>"
        table += tr
    end = "</table>"
    link = f"<a href='{qna.Truncated_info_link}'>see more</a>" if qna.Truncated_info_link else ''
    article_end = '</article>'

    return html + heading + table + end + link + article_end


def _generate_list(qna: Answer):
    html = f"""
    <article>
    <h2>{qna.question}</h2>
    """
    heading = f"<h4>{qna.answer_heading}</h4>" if qna.answer_heading else ''
    answer = '<ol>'
    for l in qna.answer:
        answer += f"<li>{l}</li>"
    answer += "</ol>"
    link = f"<a href='{qna.Truncated_info_link}'>see more</a>" if qna.Truncated_info_link else ''
    end = "</article>"

    return html + heading + answer + link + end


def _generate_youtube(qna: Answer):
    html = f"""
    <article>
    <h2>{qna.question}</h2>
    <iframe src="{qna.answer}"></iframe>
    </article>
    """
    return html
