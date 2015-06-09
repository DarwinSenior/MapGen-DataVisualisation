<listitem>
	<li class='collection-item' name='list'>
		<div onclick={toggle}>
			{ name }
			<a class="secondary-content" onclick={deletemap} href="#"><i class="fa fa-trash"></i></a>
		</div>
	</li>
	<script>
		this.id = this.opts.iid;
		this.name = this.opts.name;
		this.deletemap = function(event){
			mapActions.deleteMap(this.id);
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
	</script>
</listitem>