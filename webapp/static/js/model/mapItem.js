var mapItemStore = Reflux.createStore({
	listenables : mapItemActions,
	getItem : function(id){
		$.ajax({
			type : "GET",
			url : "/map/"+id,
			dataType : "json"
		}).success((function(data){
			this.updateItem(data, "GET");
		}).bind(this));
	},
	postItem : function(id, data){
		$.ajax({
			type : "POST",
			url : "/map/"+id,
			data : data,
			dataType : "json"
		}).success((function(data){
			this.updateItem(data, "UPDATE");
		}).bind(this));
		console.log('triggered');
	},
	updateItem : function(data, type){
		this.trigger(data, type);
	}

})