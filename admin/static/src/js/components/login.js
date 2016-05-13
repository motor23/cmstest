import React from 'react';
import {connect} from 'react-redux';
import {loginWithCredentials} from '../actions';


class Login extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    handleKeyPress(event) {
        if (event.charCode === 13) {
            event.preventDefault();
            event.stopPropagation();
            this.login();
        }
    }

    handleClick(event) {
        event.preventDefault();
        event.stopPropagation();
        this.login();
    }

    login() {
        const login = this.refs.login.value;
        const password = this.refs.password.value;
        this.props.dispatch(loginWithCredentials(login, password));
    }

    render() {
        let {error} = this.props;
        return (
            <div className="mdl-layout">
                <div className="mdl-layout__content">
                    <div className="mdl-card mdl-shadow--6dp">
                        <div className="mdl-card__title mdl-color--primary mdl-color-text--white">
                            <h2 className="mdl-card__title-text">Авторизация</h2>
                        </div>
                        <div className="mdl-card__supporting-text">
                            <form onKeyPress={this.handleKeyPress.bind(this)}>
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
                            <button className="mdl-button mdl-button--colored mdl-js-button" onClick={this.handleClick.bind(this)}>Войти</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}


const mapStateToProps = state => ({
    error: state.user.error
});


export default connect(mapStateToProps)(Login);
