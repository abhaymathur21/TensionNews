import { redirect } from "next/navigation";

const Dashboard = async () => {
  return redirect("/dashboard/latest-news");
};

export default Dashboard;
