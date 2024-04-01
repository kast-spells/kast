{{- define "concat" -}}
  {{- $parts := list . -}}
  {{- $concat := "" -}}
  {{- range $parts -}}
    {{- if ne . "" -}}
      {{- $concat = printf "%s-%s" $concat . -}}
    {{- end -}}
  {{- end -}}
  {{- printf "%s" $concat -}}
{{- end -}}