AMPY := ampy

SOURCES = \
	uclient/main.py \
	$(NULL)

__deploy__/%.py: %.py
	@mkdir -p $(dir $@)
	$(AMPY) put $< 
	@cp $< $@

deploy: $(addprefix __deploy__/, $(SOURCES))
