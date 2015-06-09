riot.tag('btn', '<a class="{\'btn-flat waves-effect waves-light\'+opts.color+\' \'+opts.classes}" onclick="{ (opts.click).bind(parent) }"> <yield></yield> </a>', function(opts) {
    	this.opts.color = this.opts.color || "";
    	this.opts.class = this.opts.class || "";
    
});