var mapActivateStore = Reflux.createStore({
	listenables : mapActivateActions,
	maps : {},
	activateMap : function(id){
		this.maps[id] = true;
		this.trigger();
	},
	deactivateMap : function(id){
		this.maps[id] = false;
		this.trigger();
	},
	activateMapList : function(){
		return mapsStore.maps.filter((function(item){
			return this.maps[item.id];
		}).bind(this));
	},
	isActivated : function(id){
		return !!this.maps[id];
	}
});