import icons from "./icons";

export default function BottomNav({ active, onNavigate }) {
  return (
    <nav className="nav" aria-label="Main">
      <button
        className={active === "camera" ? "is-active" : ""}
        onClick={() => onNavigate("camera")}
      >
        <img src={icons.camera} width="24" height="24" alt="" />
        <span>Camera</span>
      </button>

      <button
        className={active === "gallery" ? "is-active" : ""}
        onClick={() => onNavigate("gallery")}
      >
        <img src={icons.gallery} width="24" height="24" alt="" />
        <span>Gallery</span>
      </button>
    </nav>
  );
}