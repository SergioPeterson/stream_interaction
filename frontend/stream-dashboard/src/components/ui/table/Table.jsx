import * as React from "react";

export const Table = ({ children }) => (
  <table className="w-full border-collapse">{children}</table>
);

export const TableBody = ({ children }) => (
  <tbody className="divide-y">{children}</tbody>
);


export const TableRow = ({ children }) => (
  <tr className="hover:bg-gray-100">{children}</tr>
);

export const TableCell = ({ children }) => (
  <td className="p-2 border">{children}</td>
);
export const TableHead = ({ children }) => <th className="p-2 border font-bold text-left">{children}</th>;

export const TableHeader = ({ children }) => (
  <thead className="bg-gray-200">
    <tr>{children}</tr>
  </thead>
);