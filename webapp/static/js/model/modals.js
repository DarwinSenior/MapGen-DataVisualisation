var modalStore = Reflux.createStore({
	listenables : modalActions,
	onOpenModal : function(modal_id, args){
		this.trigger(modal_id, args);
	},
	onCloseModal : function(){
		this.trigger();
	}
});