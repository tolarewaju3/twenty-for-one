import React from "react";
import TimeAgo from 'react-timeago'
import {
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@material-ui/core";

// components
import { Button } from "../../../../components/Wrappers";

const states = {
  sent: "success",
  pending: "warning",
  declined: "secondary",
};

export default function TableComponent({ data }) {
  var keys = Object.keys(data[0]).map(i => i.toUpperCase());
  console.log(keys)
  keys.shift(); // delete "id" key

  return (
    <Table className="mb-0">
      <TableBody>
        {data.map(({ done_date, helper, needed_help }) => (
          <TableRow>
            <TableCell>{helper} delivered groceries to {needed_help}</TableCell>
            <TableCell><TimeAgo date={done_date}/></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
