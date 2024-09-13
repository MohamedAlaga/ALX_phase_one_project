"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { manrope } from "./layout";
import { useRouter } from "next/navigation"

export default function Home() {
  const router = useRouter();
  const handleLogin = async (e: { preventDefault: () => void; }) => {  
    e.preventDefault();
    await fetch("http://localhost:8000/api/users/current", {
      method: "GET", headers: {
        "Content-Type": "application/json",
      },credentials: "include",
    }).then((res) => res.status === 200 ? router.push("./main") : router.push("./login"))
  }
  return (
    <main className={styles.main} >
      <div className="header">
        <div className="logo"><Image src="/logo2.png" alt="logo" width={36} height={36} />
          <h1>ROLAX</h1>
        </div>
        <button className="button" onClick={handleLogin} style={{height:  36 , width:160}}><p className={manrope.className} style={{ fontSize: 14, fontWeight: 600}}>Get Started</p></button>
      </div>
      <section>
        <Image src="/onboarding.png" alt="onboarding" width={0} height={0} sizes="100vw" style={{ width: '100%', height: 'auto' }} />
      </section>
      <section>
        <h1 style={{ textAlign: "center", fontSize: 40, marginTop: 56 }}>Rolax - Feature Overview</h1>
        <div className="cardHolder" style={{  height: 210}}>
          <div className="card">
            <div className="cardText">
              <h2>
                Inventory Management
              </h2>
              <p>
                Monitor stock levels, and streamline recording processes for efficient inventory control.
              </p>
            </div>
            <Image src="/Frame3.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
          <div className="card">
            <div className="cardText">
              <h2>
                Sales Management
              </h2>
              <p>
                Manage customer orders, save all reciepts and enusre time efficient operations.
              </p>
            </div>
            <Image src="/Frame2.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
          <div className="card">
            <div className="cardText">
              <h2>
                Purchase Management
              </h2>
              <p>
                Streamline purchase orders and supplier management processes.
              </p>
            </div>
            <Image src="/Frame14.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
        </div>
      </section>
      <section>
        <h1 style={{ textAlign: "center", fontSize: 40, marginTop: 56 }}>
          About us
        </h1>
        <div className="cardHolder">
          <div className="card" style={{ boxShadow:"0px 0px 0px 0px rgba(0,0,0,0.2)" , }}>
            <Image src="/Frame4.png" width={120} height={120} alt="about us"style={{ borderRadius: 6, marginRight:16}}  />
            <p className={[styles.aboutusParagraph ,manrope.className].join(" ")} style={{marginTop: 0}}>
              ROLAX is a leading pharmacy management system, dedicated to enhancing the efficiency and accuracy of pharmacy operations. With a rich history of innovation, our mission is to provide seamless solutions that empower pharmacists and improve patient care.
            </p>
          </div></div>
      </section>
      <section className={styles.contactusSection}>
        <div className={styles.contactusWrapper}>
        <h1>
          Need to talk with us?
        </h1>
        <p className={manrope.className}>
          Get in touch with our team for any queries or support. We're here to help you!
        </p>
        <button className="button" style={{width : 132, height:52}}>
        <p className={manrope.className} style={{ fontSize: 14, fontWeight: 600 ,color:"white"}}>
          Contact us
          </p>
        </button>
        </div>
      </section>
    </main>
  );
}
