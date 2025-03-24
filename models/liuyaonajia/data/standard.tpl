{% if lunar and lunar.gz %}
阳历: {{ solar.strftime('%Y年%m月%d日 %H时') }}
干支: {{ lunar.gz.year }}年 {{ lunar.gz.month }}月 {{ lunar.gz.day }}日 {{ lunar.gz.hour }}时
{% endif %}
{% if title %}
标题: {{ title }}
{% endif %}
{% if shiy[0] %}
世爻: 第{{ shiy[0] }}爻 应爻: 第{{ shiy[1] }}爻
{% endif %}
{% for i in range(5, -1, -1) %}
{{ god6[i] }}　{{ main.mark[i] }}　{{ qin6[i] }}{{ qinx[i] }}　{{ dyao[i] }}{{ shiy[i] }}　{{ hide.qin6[i] }}　{{ bian.qin6[i] }}{{ bian.mark[i] }}
{% endfor %}
{{ main.display }}
{% if bian and bian.name and dong %}
变卦:　{{ bian.name }} ({{ bian.gong }}-{{ bian.type }})
动爻:　{%- for d in dong %} 第{{ d + 1 }}爻 {%- endfor %}
{% endif %}
{% if guaci %}
卦辞: {{ guaci }}
{% endif %}
