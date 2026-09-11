import { useEffect, useMemo, useState } from "react";

const STATUSES = ["Applied", "Interview", "Offer", "Rejected"];

function Dashboard() {
  const [applications, setApplications] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");
  const [sort, setSort] = useState("None");
  const [editingApplication, setEditingApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchApplications() {
    const token = localStorage.getItem("token");

    if (!token) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch("/applications", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to fetch applications.");
      }

      setApplications(data);
    } catch (fetchError) {
      setError(fetchError.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchApplications();

    const handleApplicationsChanged = () => {
      fetchApplications();
    };

    window.addEventListener(
      "applications-changed",
      handleApplicationsChanged
    );

    return () => {
      window.removeEventListener(
        "applications-changed",
        handleApplicationsChanged
      );
    };
  }, []);

  async function handleDelete(id) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this application?"
    );

    if (!confirmed) return;

    const token = localStorage.getItem("token");

    try {
      const response = await fetch(`/applications/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to delete application.");
      }

      await fetchApplications();
    } catch (deleteError) {
      setError(deleteError.message);
    }
  }

  function openEdit(application) {
    setEditingApplication({ ...application });
  }

  function updateEditingField(event) {
    setEditingApplication({
      ...editingApplication,
      [event.target.name]: event.target.value,
    });
  }

  async function saveEdit(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        `/applications/${editingApplication.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            company: editingApplication.company,
            role: editingApplication.role,
            status: editingApplication.status,
            notes: editingApplication.notes || "",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to update application.");
      }

      setEditingApplication(null);
      await fetchApplications();
    } catch (updateError) {
      setError(updateError.message);
    }
  }

  const filteredApplications = useMemo(() => {
    const normalizedSearch = search.toLowerCase().trim();

    const filtered = applications.filter((application) => {
      const matchesSearch =
        application.company.toLowerCase().includes(normalizedSearch) ||
        application.role.toLowerCase().includes(normalizedSearch);

      const matchesStatus =
        filter === "All" || application.status === filter;

      return matchesSearch && matchesStatus;
    });

    return [...filtered].sort((first, second) => {
      if (sort === "Company") {
        return first.company.localeCompare(second.company);
      }

      if (sort === "Role") {
        return first.role.localeCompare(second.role);
      }

      if (sort === "Oldest") {
        return first.id - second.id;
      }

      return second.id - first.id;
    });
  }, [applications, search, filter, sort]);

  const total = applications.length;
  const offers = applications.filter(
    (application) => application.status === "Offer"
  ).length;
  const interviews = applications.filter(
    (application) => application.status === "Interview"
  ).length;
  const rejected = applications.filter(
    (application) => application.status === "Rejected"
  ).length;

  return (
    <section className="card dashboard-card">
      <div className="dashboard-heading">
        <div>
          <p className="eyebrow">Overview</p>
          <h2>My Applications</h2>
        </div>

        <span className="application-count">
          {total} {total === 1 ? "application" : "applications"}
        </span>
      </div>

      <div className="stats">
        <div className="stat-card">
          <span>Total</span>
          <strong>{total}</strong>
        </div>

        <div className="stat-card">
          <span>Interviews</span>
          <strong>{interviews}</strong>
        </div>

        <div className="stat-card">
          <span>Offers</span>
          <strong>{offers}</strong>
        </div>

        <div className="stat-card">
          <span>Rejected</span>
          <strong>{rejected}</strong>
        </div>
      </div>

      <div className="toolbar">
        <input
          type="search"
          placeholder="Search by company or role"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <select
          value={filter}
          onChange={(event) => setFilter(event.target.value)}
        >
          <option value="All">All statuses</option>

          {STATUSES.map((status) => (
            <option value={status} key={status}>
              {status}
            </option>
          ))}
        </select>

        <select
          value={sort}
          onChange={(event) => setSort(event.target.value)}
        >
          <option value="None">Sort applications</option>
          <option value="Oldest">Oldest first</option>
          <option value="Company">A–Z by company</option>
          <option value="Role">A–Z by role</option>
        </select>
      </div>

      {error && <p className="error-msg">{error}</p>}

      {loading ? (
        <p className="empty-msg">Loading applications...</p>
      ) : filteredApplications.length === 0 ? (
        <p className="empty-msg">
          {applications.length === 0
            ? "No applications yet. Add one above!"
            : "No applications match your search or filter."}
        </p>
      ) : (
        <div className="applications-list">
          {filteredApplications.map((application) => (
            <article className="app-item" key={application.id}>
              <div className="app-info">
                <h3>
                  {application.company} — {application.role}
                </h3>

                <p>{application.notes || "No notes added"}</p>
              </div>

              <div className="app-actions">
                <span
                  className={`status-badge status-${application.status}`}
                >
                  {application.status}
                </span>

                <button
                  className="edit-btn"
                  onClick={() => openEdit(application)}
                >
                  Edit
                </button>

                <button
                  className="delete-btn"
                  onClick={() => handleDelete(application.id)}
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {editingApplication && (
        <div className="modal">
          <form className="modal-content" onSubmit={saveEdit}>
            <h2>Edit Application</h2>

            <input
              type="text"
              name="company"
              value={editingApplication.company}
              onChange={updateEditingField}
              placeholder="Company"
              required
            />

            <input
              type="text"
              name="role"
              value={editingApplication.role}
              onChange={updateEditingField}
              placeholder="Role"
              required
            />

            <select
              name="status"
              value={editingApplication.status}
              onChange={updateEditingField}
            >
              {STATUSES.map((status) => (
                <option value={status} key={status}>
                  {status}
                </option>
              ))}
            </select>

            <input
              type="text"
              name="notes"
              value={editingApplication.notes || ""}
              onChange={updateEditingField}
              placeholder="Notes"
            />

            <div className="modal-buttons">
              <button type="submit">Save changes</button>

              <button
                type="button"
                className="cancel-btn"
                onClick={() => setEditingApplication(null)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
    </section>
  );
}

export default Dashboard;