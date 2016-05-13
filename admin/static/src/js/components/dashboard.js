import React from 'react';
import {connect} from 'react-redux';
import Spinner from './spinner';


class MenuItem_Stream extends React.Component {
    render() {
        const {title} = this.props;
        return (
            <button className="mdl-button mdl-js-button">{title}</button>
        );
    }
}


class MenuItem extends React.Component {
    render() {
        const {title, children} = this.props;
        return (
            <div className="mdl-card">
                <div className="mdl-card__title">{title}</div>
                <div className="mdl-card__actions mdl-card--border">
                    {children.map(child => <MenuItem_Stream key={child.title} {...child} />)}
                </div>
            </div>
        );
    }
}


class Dashboard extends React.Component {
    render() {
        const {dashboard} = this.props;

        if (!dashboard) {
            return <Spinner/>;
        }

        return (
            <div>
                {dashboard.map(child => <MenuItem key={child.title} {...child} />)}
            </div>
        );
    }
}


const mapStateToProps = state => ({
    dashboard: state.config.menu.dashboard
});


export default connect(mapStateToProps)(Dashboard);