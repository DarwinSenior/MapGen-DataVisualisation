var mapsStore = Reflux.createStore({
	listenables : mapActions,
	maps : [],
	addMap : function(data){
		console.log("add map");
		$.ajax({
			type: "PUT",
			url: "/maps",
			data : data,
			contentType : false,
			processData : false,
			dataType : "json"
		}).success((function(data){
			this.updateMaps(data);
		}).bind(this));
	},
	deleteMap : function(id){
		$.ajax({
			type : "DELETE",
			url : "/maps",
			data : {id : id},
			dataType : "json"
		}).success((function(data){
			this.updateMaps(data);
			console.log(data);
		}).bind(this));
	},
	getMaps : function(){
		$.ajax({
			type : "GET",
			url : "/maps",
			dataType : "json"
		}).success((function(data){
			this.updateMaps(data);
		}).bind(this))
	},
	updateMaps : function(new_maps){
		// compare the difference
		var old_set = {};
		this.maps.forEach(function(item){
			old_set[item.id] = true;
		});
		var new_set = {};

		new_maps.forEach(function(item){
			new_set[item.id] = true;
		})

		var entermaps = new_maps.filter(function(item){
			return !old_set[item.id];
		});
		var exitmaps = this.maps.filter(function(item){
			return !new_set[item.id];
		});
		var updatemaps = new_maps.filter(function(item){
			return old_set[item.id];
		});
		this.maps = new_maps;
		this.trigger(new_maps, updatemaps, entermaps, exitmaps);
	}
});