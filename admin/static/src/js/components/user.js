import React from 'react';
import {logout} from '../actions';


class User extends React.Component {
    static propTypes = {
        name: React.PropTypes.object.isRequired,
        logout: React.PropTypes.func.isRequired
    };

    render() {
        const {name, logout} = this.props;
        return (
            <div className="cms-user">
                <b className="cms-user__name">Привет, {name}</b>
                <i className="cms-user__logout" onClick={logout}>Выйти</i>
            </div>
        );
    }
}


export default User;