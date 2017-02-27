import React, {Component, PropTypes} from 'react';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import Spinner from './common/spinner';




export class StreamItem extends Component {
    static propTypes = {
        id: PropTypes.string.isRequired,
        stream: PropTypes.string.isRequired
    };

    componentWillMount() {
        const {actions, id, stream} = this.props;
        actions.fetchStreamItem({id, stream});
    }

    componentWillReceiveProps(nextProps) {
        const {actions, id, stream} = this.props;
        if (nextProps.id !== id || nextProps.stream !== stream) {
            actions.fetchStreamItem({id: nextProps.id, stream: nextProps.stream});
        }
    }

    render() {
        return (
            <div>
                <div>Item: {this.props.id}</div>
            </div>
        );
    }
}


export function mapStateToProps(state, ownProps) {
    return {
        id: ownProps.match.params.id,
        stream: ownProps.match.params.stream
    };
}


export function mapDispatchToProps(dispatch, ownProps) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(StreamItem);