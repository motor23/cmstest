import React from 'react';
import {connect} from 'react-redux';
import {updateStreamList} from '../../actions';
import Spinner from '../spinner';


class Paginator extends React.Component {
    static propTypes = {
        total: React.PropTypes.number.isRequired,
        limit: React.PropTypes.number.isRequired,
        offset: React.PropTypes.number.isRequired
    };

    render() {
        return (
            <div className="cms-paginator">
            </div>
        );
    }
}


class StreamListRow extends React.Component {
    render() {
        const {item} = this.props;
        return (
            <tr>
                <td>{item.id}</td>
                <td>{item.title}</td>
            </tr>
        );
    }
}


class StreamList extends React.Component {
    static propTypes = {
        isLoading: React.PropTypes.bool.isRequired,
        widgets: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        filters: React.PropTypes.object.isRequired,
        errors: React.PropTypes.object.isRequired,
        items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
        total: React.PropTypes.number.isRequired,
        limit: React.PropTypes.number.isRequired,
        offset: React.PropTypes.number.isRequired
    };

    componentWillMount() {
        this.props.dispatch(updateStreamList('docs', 30));
    }

    render() {
        const {isLoading, items} = this.props;
        const content = items.map(item => <StreamListRow key={item.id} item={item}/>);
        if (isLoading) {
            return <Spinner/>;
        }
        return (
            <table className="mdl-data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Заголовок</th>
                    </tr>
                </thead>
                <tbody>
                    {content}
                </tbody>
            </table>
        );
    }
}


function mapStateToProps(state, props) {
    return {
        isLoading: state.stream.isLoading,
        items: state.stream.items,
        filters: state.stream.filters,
        errors: state.stream.errors,
        total: state.stream.total,
        limit: state.stream.limit,
        offset: state.stream.offset
    };
}


export default connect(mapStateToProps)(StreamList);