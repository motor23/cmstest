import React, {Component, PropTypes} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import {Link} from 'react-router-dom';
import Spinner from './common/spinner';


export class StreamItem extends Component {
    static propTypes = {
        title: PropTypes.string.isRequired,
        stream: PropTypes.string.isRequired
    };

    render() {
        const {title, stream} = this.props;
        return (
            <div className="cms-card__item">
                <Link to={`streams/${stream}/`}>{title}</Link>
            </div>
        );
    }
}


export class Card extends Component {
    render() {
        const {title, children} = this.props;
        const content = children.map(child =>
                <StreamItem key={child.title} {...child}/>
        );
        return (
            <div className="cms-card mdl-shadow--2dp">
                <div className="cms-card__title">{title}</div>
                {content}
            </div>
        );
    }
}


export class Dashboard extends Component {
    static propTypes = {
        dashboard: PropTypes.object.isRequired
    };

    render() {
        const {dashboard} = this.props;
        const content = dashboard.map(child =>
                <Card key={child.title} {...child}/>
        );
        return (
            <div className="cms-dashboard">
                {content}
            </div>
        );
    }
}


export function mapStateToProps(state) {
    return {
        dashboard: state.app.cfg.menu.dashboard
    };
}


export function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(Dashboard)
