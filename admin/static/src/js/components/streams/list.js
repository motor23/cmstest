import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {updateStreamList} from '../../actions/stream';
import paginate from '../../util/paginate';
import Spinner from '../spinner';


class Paginator extends Component {
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
        console.log(pages)
        return (
            <div className="cms-paginator">
                {pages.map(this.renderItem.bind(this))}
            </div>
        );
    }
}


class StreamListRow extends Component {
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


class StreamList extends Component {
    static propTypes = {
        isLoading: PropTypes.bool.isRequired,
        widgets: PropTypes.arrayOf(PropTypes.object).isRequired,
        filters: PropTypes.object.isRequired,
        errors: PropTypes.object.isRequired,
        items: PropTypes.arrayOf(PropTypes.object).isRequired,
        total: PropTypes.number.isRequired,
        pageSize: PropTypes.number.isRequired,
        page: PropTypes.number.isRequired
    };

    componentWillMount() {
        const {stream, page, pageSize} = this.props;
        this.props.dispatch(updateStreamList(stream, page, pageSize));
    }

    changePage(page) {
        const {pageSize} = this.props;
        this.props.dispatch(updateStreamList('docs', page, pageSize));
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


function mapStateToProps(state, props) {
    return {
        stream: props.params.stream,
        isLoading: state.stream.isLoading,
        title: state.stream.title,
        items: state.stream.items,
        filters: state.stream.filters,
        errors: state.stream.errors,
        total: state.stream.total,
        pageSize: state.stream.pageSize,
        page: state.stream.page
    };
}


export default connect(mapStateToProps)(StreamList);