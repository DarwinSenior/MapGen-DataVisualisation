var mapsStore = Reflux.createStore({
	listenables : mapActions,
	maps : [],
	addMap : function(name, file){
		$.ajax({
			type: "PUT",
			url: "/maps",
			data : {name : name},
			dataType : "json"
		}).done((function(newmap){
			data = new FormData();
			data.append('csv', file);
			this.updateMaps(newmap);
			_id = _.find(newmap, function(value){return (value.status=="uninitiated" && value.name==name)}).id;
			console.log(_id);
			data.append('id', _id);
			this.initMaps(data, _id);
		}).bind(this));
	},
	deleteMap : function(id){
		$.ajax({
			type : "DELETE",
			url : "/maps",
			data : {id : id},
			dataType : "json"
		}).done((function(data){
			this.updateMaps(data);
		}).bind(this));
	},
	initMaps : function(data, _id){
		$.ajax({
			type: "POST",
			url: "/maps/load",
			data : data,
			contentType : false,
			processData : false,
			dataType : 'json'
		}).done((function(data){
			this.updateMaps(data);
		}).bind(this)).fail((function(err){
			console.log(err);
			this.deleteMap(_id);
		}).bind(this));
	},
	getMaps : function(){
		$.ajax({
			type : "GET",
			url : "/maps",
			dataType : "json"
		}).done((function(data){
			this.updateMaps(data);
		}).bind(this))
	},
	updateMaps : function(new_maps){
		console.log(new_maps);
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