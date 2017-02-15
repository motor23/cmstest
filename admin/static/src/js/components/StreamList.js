import React, {Component, PropTypes} from 'react';
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
                <span className="cms-paginator__item cms-paginator__item--ellipsis">
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
        const {item} = this.props;
        return (
            <tr>
                <td>{item.id}</td>
                <td>{item.title.substring(0, 100)}</td>
            </tr>
        );
    }
}


export class StreamList extends Component {
    static propTypes = {
        actions: PropTypes.object.isRequired,
        isLoading: PropTypes.bool.isRequired,
        filters: PropTypes.object.isRequired,
        errors: PropTypes.object.isRequired,
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
        const {isLoading, title, items, total, pageSize, page} = this.props;
        const content = items.map(item => <StreamListRow key={item.id} item={item}/>);
        if (isLoading) {
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
        stream: ownProps.params.stream,
        isLoading: state.stream.isLoading,
        title: state.stream.title,
        items: state.stream.items,
        filters: state.stream.filters,
        errors: state.stream.errors,
        total: state.stream.total,
        pageSize: state.stream.pageSize,
        page: state.stream.page,
        order: state.stream.order
    };
}


export function mapDispatchToProps(dispatch, ownProps) {
    return {
        ...ownProps,
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(StreamList);