export const Card = ({ children }) => (
    <div className="bg-white rounded-lg shadow-md p-4">{children}</div>
  );
  
  export const CardHeader = ({ children }) => (
    <div className="font-bold text-lg mb-2">{children}</div>
  );
  
  export const CardContent = ({ children }) => (
    <div className="text-gray-700">{children}</div>
  );