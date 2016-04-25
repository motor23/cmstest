import React from 'react';


class Login extends React.Component {
    static contextTypes = {
        connection: React.PropTypes.object.isRequired,
        router: React.PropTypes.object.isRequired
    };

    constructor(props, context) {
        super(props, context);
        this.state = {error: ''};
    }

    componentWillMount() {
        this.subscription_ok = this.context.connection
            .receive('auth.login_ok', this.handleSuccess.bind(this));
        this.subscription_error = this.context.connection
            .receive('auth.login_error', this.handleError.bind(this));
    }

    componentWillUnmount() {
        this.subscription_ok.unsubscribe();
        this.subscription_error.unsubscribe()
    }

    handleError(body) {
        this.setState({error: 'Неверный логин или пароль'});
    }

    handleSuccess(body) {
        window.loggedIn = true;
        this.context.router.replace('/dashboard');
    }

    login(event) {
        event.preventDefault();
        let login = this.refs.login.value;
        let password = this.refs.password.value;
        this.context.connection.send('auth.login', {login, password});
        this.setState({isLoggingIn: true});
    }

    render() {
        let {error} = this.state;
        return (
            <div className="mdl-layout__content">
                <div className="mdl-card mdl-shadow--6dp">
                    <div className="mdl-card__title mdl-color--primary mdl-color-text--white">
                        <h2 className="mdl-card__title-text">Авторизация</h2>
                    </div>
                    <div className="mdl-card__supporting-text">
                        <form>
                            <div className="mdl-textfield mdl-js-textfield">
                                <input className="mdl-textfield__input" type="text" ref="login" id="login"/>
                                <label className="mdl-textfield__label" for="login">Логин</label>
                                {error ? <span class="mdl-textfield__error">{error}</span> : null}
                            </div>
                            <div className="mdl-textfield mdl-js-textfield">
                                <input className="mdl-textfield__input" type="password" ref="password" id="password"/>
                                <label className="mdl-textfield__label" for="login">Пароль</label>
                                {error ? <span class="mdl-textfield__error">{error}</span> : null}
                            </div>
                        </form>
                    </div>
                    <div className="mdl-card__actions mdl-card--border">
                        <button className="mdl-button mdl-button--colored mdl-js-button" onClick={this.login.bind(this)}>Войти</button>
                    </div>
                </div>
            </div>
        )
    }
}


export default Login;
