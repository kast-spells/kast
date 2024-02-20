{{/*kast - Kubernetes arcane spelling technology
Copyright (C) 2023 namenmalkv@gmail.com

This work is licensed under the Creative Commons Attribution-ShareAlike 
NonCommercial (CC BY-SA-NC) license. See the LICENSE file for details. */}}
{{- define "glyph.runicIndexer" -}}
{{- $glyphs := index . 0 -}}
{{- $selectors := index . 1 -}}
{{- $type := index . 2 -}}
{{- $chapter := index . 3 -}}
{{- $results := list -}}
{{- $bookDefault := list -}}
{{- $chapterDefault := list -}}

{{- range $currrentGlyph := $glyphs -}}
  {{- if eq $currrentGlyph.type $type -}}
    {{- range $selector, $value := $selectors -}}
      {{- if (hasKey $currrentGlyph.labels $selector) -}}
        {{- if eq (index $currrentGlyph.labels $selector) $value -}}
            {{- $results = append $results $currrentGlyph -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
    {{- if and (hasKey $currrentGlyph.labels "default") (eq (len $results) 0) -}}
      {{- if eq (index $currrentGlyph.labels "default") "book" -}}
        {{- $bookDefault = append $bookDefault $currrentGlyph -}}
      {{- else if and (eq $currrentGlyph.chapter $chapter) (eq (index $currrentGlyph.labels "default") "chapter") -}}
        {{- $chapterDefault = append $chapterDefault $currrentGlyph -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if (eq (len $results) 0) -}}
  {{- if (eq (len $chapterDefault) 0) -}}
    {{- $results = $bookDefault -}}
  {{- else -}}
    {{- $results = $chapterDefault -}}
  {{- end -}}
{{- end -}}
{{- dict "results" $results | toJson -}}
{{- end -}}