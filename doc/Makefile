defaults: usage_append.html usage_delfields.html usage_execc.html usage_filter.html usage_checkdups.html usage_merge.html usage_read.html usage_render.html usage_rewrite.html usage_sort.html usage_unappend.html

usage_%.html: templates/usage.md makeref.py
	python makeref.py $(*F) | markdown_py > $@ 
	test ! -f extra/extra_$(*F).txt || cat extra/extra_$(*F).txt | markdown_py >> $@

