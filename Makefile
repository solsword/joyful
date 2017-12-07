out/test-assoc.txt: joyful.py test/test.csv out
	sed test/test.csv -e "s/^[^,]*,[^,]*,//" \
		| tr -d '"' \
		| ./joyful.py \
		> out/test-assoc.txt

out/test-entropy.txt: joyful.py test/test.csv out
	sed test/test.csv -e "s/^[^,]*,[^,]*,//" \
		| tr -d '"' \
		| ./joyful.py -e \
		> out/test-entropy.txt

out/gods-assoc.txt: joyful.py test/the-gods-of-pegana.txt out
	cat test/the-gods-of-pegana.txt \
		| ./sentences.py 2> out/gods-warnings.txt \
		| tr -d "\"',:;?!.*" \
		| ./joyful.py \
		> out/gods-assoc.txt

out/gods-entropy.txt: joyful.py test/the-gods-of-pegana.txt out
	cat test/the-gods-of-pegana.txt \
		| ./sentences.py 2> out/gods-warnings.txt \
		| tr -d "\"',:;?!.*" \
		| ./joyful.py -e \
		> out/gods-entropy.txt

out:
	mkdir -p out

.PHONY: tests
tests: out/test-assoc.txt out/test-entropy.txt out/gods-assoc.txt out/gods-entropy.txt

.PHONY: clean
clean: rm -f out/*
