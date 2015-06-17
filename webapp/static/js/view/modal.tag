<modal>
	<div class="modal" name="modal">
		<yield />
	</div>
	<script>
		this.visible = false;
		this.id = this.opts.mid;
		this.args = {};
		this.change = function(id, args){
			if (id == this.id){
				$(this.modal).openModal();
				this.args = args;
				this.update();
			} else {
				$(this.modal).closeModal();
				this.update();
			}
		}
		modalStore.listen((this.change).bind(this));
	</script>
</modal>