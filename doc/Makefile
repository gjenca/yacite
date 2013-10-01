.PRECIOUS: usage_*.html

defaults:tutorial.html reference.html

usage_%.html: templates/usage.md makeref.py ../yacite/command/%.py extra/extra_%.txt
	python makeref.py $(*F) | markdown_py > $@ 
	test ! -f extra/extra_$(*F).txt || cat extra/extra_$(*F).txt | markdown_py >> $@

tutorial.html: tutorial.txt
	markdown_py tutorial.txt > $@

bib2yaml.html: bib2yaml.txt
	markdown_py bib2yaml.txt > $@

reference.html: bib2yaml.html usage_append.html usage_delfields.html usage_execc.html usage_filter.html usage_checkdups.html usage_merge.html usage_read.html usage_render.html usage_rewrite.html usage_sort.html usage_unappend.html 
	bash makeref_all > $@

