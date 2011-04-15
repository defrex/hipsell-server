//depends: main.js, core/auth/dialog.js

hs._Auth = function(){
    if (hs.auth instanceof hs._Auth)
        throw('hs._Auth is not to be instantiated other then for hs.auth');
    
    this.token = localStorage.getItem('token');
    _.extend(this, Backbone.Events);
};

hs._Auth.prototype.isAuthenticated = function(){
    return typeof this.token == 'string';
};

hs._Auth.prototype.authenticated = function(clbk, context){
    clbk = _.bind(clbk, context);
    if (this.isAuthenticated()){
        clbk();
        return this;
    }
    if (typeof this.email == 'undefined')
        this._loginPrompt(clbk);
    else
        this._createUser(clbk);
    return this;
};

hs._Auth.prototype.setEmail = function(email){
    this.email = email;
    this.trigger('change:email');
    return this;
};

hs._Auth.prototype._createUser = function(clbk){
    if (typeof this.email == 'undefined')
        throw('cannot create a user with no email');
    $.ajax({
        url: '/api/v1/user/', 
        data: JSON.stringify({username: this.email}), 
        contentType: 'application/json',
        type: 'POST',
        context: this,
        complete: function(jqXHR){
            if (jqXHR.status == 201){
                hs.log('201', jqXHR);
                this.token = JSON.parse(jqXHR.responseText).token;
                localStorage.setItem('token', this.token);
                this.trigger('change:isAuthenticated', [true]);
                clbk();
            }else{
                hs.log('err', jqXHR);
                hs.log('TODO: password prompt and login');
            }
        }
    });
    return this;
};

hs._Auth.prototype._loginPrompt = function(clbk){
    var dialog = new hs.auth.Dialog();
    dialog.bind('set:email', _.bind(function(email){
        this.setEmail(email);
        this._createUser(function(){
            dialog.remove();
            clbk();
        });
    }, this));
    dialog.render();
    return this;
};

hs._Auth.prototype.logout = function(){
    this.token = undefined;
    this.email = undefined;
    this.trigger('change:isAuthenticated', [false]);
    return this;
};

hs.auth = _.extend(hs.auth || new Object(), new hs._Auth());