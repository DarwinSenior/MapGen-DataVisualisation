riot.tag('listitem', '<li class="collection-item" name="list"> <div if="{opts.status!=\'ready\'}" class="grey"> <div class="progress"> <div class="indeterminate"></div> </div> </div> <div onclick="{toggle}" if="{opts.status==\'ready\'}"> { name } <div class="secondary-content"> <a onclick="{modifymap}" href="#"> <i class="fa fa-pencil"></i> </a> <a onclick="{deletemap}" href="#"> <i class="fa fa-trash"></i> </a> </div> </div> </li>', function(opts) {
		this.id = this.opts.iid;
		this.name = this.opts.name;
		this.deletemap = function(event){

			modalActions.openModal("deleteMap", {id : this.id, name: this.name});
			event.stopPropagation();
		}
		this.modifymap = function(modifymap){
			modalActions.openModal("modifyMap", {id : this.id, name: this.name});
			event.stopPropagation();
		}

		this.toggle = function(event){
			if (this.opts.activated){
				mapActivateActions.deactivateMap(this.id);
			}else{
				mapActivateActions.activateMap(this.id);
			}
		}
		this.on('updated', (function(){
			d3.select(this.list).transition()
				.style('background-color', !this.opts.activated ? 'white' : 'black')
				.style('color', !this.opts.activated ? 'black' : 'white');
		}).bind(this));
	
});