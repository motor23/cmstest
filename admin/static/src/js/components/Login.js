import React, {Component, PropTypes} from 'react';


export default class Login extends Component {
    static propTypes = {
        actions: React.PropTypes.object.isRequired,
    };

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
        const {actions} = this.props;
        actions.login({login: login, password: password});
    }

    render() {
        let {error} = this.props;
        return (
            <div className="slds-modal slds-fade-in-open">
                <div className="slds-modal__container">
                    <div className="slds-modal__header">
                        <h2 className="slds-text-heading--medium">Авторизация</h2>
                    </div>
                    <div className="slds-modal__content">
                        <form className="slds-form--horizontal" onKeyPress={this.handleKeyPress}>
                            <div className={'slds-form-element' + (error ? ' slds-has-error' : '')}>
                                <label className="slds-form-element__label" htmlFor="login">Логин</label>
                                <div className="slds-form-element__control">
                                    <input className="slds-input" type="text" ref="login" id="login"/>
                                </div>
                                {error ? <div class="sld-form-element__error">{error}</div> : null}
                            </div>
                            <div className={'slds-form-element' + (error ? ' slds-has-error' : '')}>
                                <label className="slds-form-element__label" htmlFor="login">Пароль</label>
                                <div className="slds-form-element__control">
                                    <input className="slds-input" type="password" ref="password" id="password"/>
                                </div>
                                {error ? <div class="slds-form-element__error">{error}</div> : null}
                            </div>
                        </form>
                    </div>
                    <div className="slds-modal__footer">
                        <button className="slds-button slds-button--brand" onClick={this.handleClick}>Войти</button>
                    </div>
                </div>
            </div>
        );
    }
}
