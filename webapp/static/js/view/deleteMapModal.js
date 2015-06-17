
riot.tag('delete-file', '<div class="modal-content">  <h5>Are you sure you want to delete the following file?</h5> <h5>{name || \'undefined\'}</h5> </div> <div class="modal-footer"> <btn click="{cancel}">Cancel <i class="fa fa-times"></i></btn> <btn click="{okay}">OK <i class="fa fa-check"></i></btn> </div>', function(opts) {
		this.getArgs = function(){
			var args = this.parent.args;
			this.name = args.name;
			this.id = args.id;
		}
		this.okay = function(){
			mapActions.deleteMap(this.id);
			modalActions.closeModal();
		}
		this.cancel = function(){
			this.name = undefined;
			this.id = undefined;
			modalActions.closeModal();
		}
		this.on("update", (this.getArgs).bind(this));
	
});