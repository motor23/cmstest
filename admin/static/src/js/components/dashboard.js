import React from 'react';
import {Link} from 'react-router';
import {connect} from 'react-redux';
import Spinner from './spinner';


class StreamItem extends React.Component {
    static propTypes = {
        title: React.PropTypes.string.isRequired,
        stream: React.PropTypes.string.isRequired
    };

    render() {
        const {title, stream} = this.props;
        return (
            <div className="cms-card__item">
                <Link to={`/${stream}/`}>{title}</Link>
            </div>
        );
    }
}


class Card extends React.Component {
    render() {
        const {title, children} = this.props;
        const content = children.map(child => <StreamItem key={child.title} {...child} />);
        return (
            <div className="cms-card mdl-shadow--2dp">
                <div className="cms-card__title">{title}</div>
                {content}
            </div>
        );
    }
}


class Dashboard extends React.Component {
    render() {
        const {dashboard} = this.props;
        const content = dashboard.map(child => <Card key={child.title} {...child} />);
        return (
            <div className="cms-dashboard">
                {content}
            </div>
        );
    }
}


function mapStateToProps(state, props) {
    return {
        dashboard: state.conf.dashboard
    };
}


export default connect(mapStateToProps)(Dashboard);