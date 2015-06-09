riot.tag('listview', '<div each="{items}" class="card-panel"> <div class="center-align"> {name} </div> <div class="section"></div> <mapview iid="{id}" syncmaps="{parent.syncmaps}"></mapview> </div>', function(opts) {
		this.items = mapActivateStore.activateMapList();
		this.updateList = function(){
			this.items = mapActivateStore.activateMapList();
			this.update();
			$(this.collapsible).collapsible();
		}
		this.syncmaps = {};
		mapActivateStore.listen((this.updateList).bind(this));
	
});