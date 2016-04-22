import React from 'react';


class Login extends React.Component {
    render() {
        return (
            <div className="mdl-layout__content">
                <div className="mdl-grid">
                    <form className="mdl-cell mdl-cell--12-col">
                        <div className="mdl-textfield mdl-js-textfield">
                            <input className="mdl-textfield__input" type="text" ref="login" id="login"/>
                            <label className="mdl-textfield__label" for="login">Логин</label>
                        </div>
                        <div className="mdl-textfield mdl-js-textfield">
                            <input className="mdl-textfield__input" type="password" ref="password" id="password"/>
                            <label className="mdl-textfield__label" for="login">Пароль</label>
                        </div>
                        <button className="mdl-button mdl-js-button">Войти</button>
                    </form>
                </div>
            </div>
        )
    }
}


export default Login;
