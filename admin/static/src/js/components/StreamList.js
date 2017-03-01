import React, {Component, PropTypes} from 'react';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import paginate from '../util/paginate';
import Spinner from './common/spinner';


export class Paginator extends Component {
    static propTypes = {
        total: PropTypes.number.isRequired,
        page: PropTypes.number.isRequired,
        pageSize: PropTypes.number.isRequired,
        change: PropTypes.func.isRequired
    };

    renderItem(n) {
        const {page, change} = this.props;
        if (n === page) {
            return (
                <span key={n} className="cms-paginator__item cms-paginator__item--current">
                    {n}
                </span>
            );
        }
        if (n === null) {
            return (
                <span key="ellipsis" className="cms-paginator__item cms-paginator__item--ellipsis">
                    &hellip;
                </span>
            );
        }
        return (
            <span key={n} className="cms-paginator__item" onClick={() => change(n)}>
                {n}
            </span>
        );
    }

    render() {
        const {total, page, pageSize} = this.props;
        const pages = paginate(total, pageSize, page, 1, 3);
        return (
            <div className="cms-paginator">
                {pages.map(this.renderItem.bind(this))}
            </div>
        );
    }
}


export class StreamListRow extends Component {
    render() {
        const {item, stream} = this.props;
        return (
            <tr>
                <td><Link to={`/streams/${stream}/${item.id}/`}>{item.id}</Link></td>
                <td><Link to={`/streams/${stream}/${item.id}/`}>{item.title.substring(0, 100)}</Link></td>
            </tr>
        );
    }
}


export class StreamList extends Component {
    static propTypes = {
        actions: PropTypes.object.isRequired,
        loading: PropTypes.bool.isRequired,
        filters: PropTypes.object.isRequired,
        items: PropTypes.arrayOf(PropTypes.object).isRequired,
        total: PropTypes.number.isRequired,
        pageSize: PropTypes.number.isRequired,
        page: PropTypes.number.isRequired,
        order: PropTypes.string.isRequired
    };

    constructor(props) {
        super(props);
        this.onKeyPress = this.onKeyPress.bind(this);
    }

    componentWillMount() {
        const {stream, page, pageSize, actions} = this.props;
        actions.streamList({stream, page, pageSize});
    }

    componentWillReceiveProps(nextProps) {
        const {stream, actions} = this.props;
        if (nextProps.stream !== stream) {
            actions.streamList({stream: nextProps.stream, page: 1, pageSize: nextProps.pageSize});
        }
    }

    componentDidMount() {
        window.addEventListener('keydown', this.onKeyPress, true);
    }

    componentWillUnmount() {
        window.removeEventListener('keydown', this.onKeyPress, true);
    }

    onKeyPress(event) {
        if (event.keyCode == 37) {
            this.changePageToPrev();
        }
        if (event.keyCode == 39) {
            this.changePageToNext();
        }
    }

    changePageToPrev() {
        const {page} = this.props;
        if (page > 1) {
            this.changePage(page - 1);
        }
    }

    changePageToNext() {
        const {page, total, pageSize} = this.props;
        if (page < total / pageSize) {
            this.changePage(page + 1);
        }
    }

    changePage(page) {
        const {stream, pageSize, actions} = this.props;
        actions.streamList({stream, page, pageSize});
    }

    render() {
        const {loading, title, items, total, pageSize, page, stream} = this.props;
        const content = items.map(item => <StreamListRow key={item.id} item={item} stream={stream}/>);
        if (loading) {
            return <Spinner/>;
        }
        return (
            <div className="cms-stream">
                <div className="slds-page-header">
                    <div className="slds-page-header__title">{title}</div>
                </div>
                <table className="slds-table slds-table--bordered">
                    <thead>
                    <tr className="slds-text-heading--label">
                        <th>ID</th>
                        <th>Заголовок</th>
                    </tr>
                    </thead>
                    <tbody>
                    {content}
                    </tbody>
                </table>
                <Paginator total={total} page={page} pageSize={pageSize} change={this.changePage.bind(this)}/>
            </div>
        );
    }
}


export function mapStateToProps(state, ownProps) {
    return {
        stream: ownProps.match.params.stream,
        loading: state.list.loading,
        title: state.list.title,
        items: state.list.items,
        filters: state.list.filters,
        total: state.list.total,
        pageSize: state.list.pageSize,
        page: state.list.page,
        order: state.list.order
    };
}


export function mapDispatchToProps(dispatch, ownProps) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(StreamList);