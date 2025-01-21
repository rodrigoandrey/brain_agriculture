import io
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger('django')

def generate_pie_chart(data, labels, title):  # NOQA
    logger.info("Iniciando a geração do gráfico: %s", title)
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf
