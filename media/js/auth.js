//depends: main.js

hs._Auth = function(){
    if (hs.auth instanceof hs._Auth)
        throw('hs._Auth is not to be instantiated other then for hs.auth');

    this.token = CONST.apiToken;
};

hs._Auth.prototype.isAuthenticated = function(){
    return typeof this.token == 'string';
};

hs._Auth.prototype.authenticated = function(clbk){
    if (this.isAuthenticated()){
        if (clbk) clbk.call(this);
        return this;
    }
    var auth = this;

    $.ajax({
        url: '/api/v1/user/', 
        data: JSON.stringify({email: this.email}), 
        contentType: 'application/json',
        type: 'POST',
        complete: function(data, textStatus, jqXHR){
            if (jqXHR.status == 200){
                hs.log('200', data);
                auth.token = data.token;
                if (clbk) clbk.call(auth);
            }else{
                hs.log('err', jqXHR);
                hs.log('TODO: password prompt and login');
            }
        }
    });

    return this;
};

hs._Auth.prototype.setEmail = function(email){
    this.email = email;
}

hs.auth = new hs._Auth();