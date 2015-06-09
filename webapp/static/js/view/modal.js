riot.tag('modal', '<div class="modal" name="modal"> <yield ></yield> </div>', function(opts) {
		this.visible = false;
		this.id = this.opts.mid;
		this.change = function(id, args){
			if (id == this.id){
				$(this.modal).openModal();
				this.args = args;
			} else {
				$(this.modal).closeModal();
			}
		}
		modalStore.listen((this.change).bind(this));
	
});