"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { manrope, lexend } from "./layout";
import { useRouter } from "next/navigation"

export default function Home() {
  const router = useRouter();
  const handleLogin = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    await fetch("http://localhost:8000/api/users/current", {
      method: "GET", headers: {
        "Content-Type": "application/json",
      }, credentials: "include",
    }).then((res) => res.status === 200 ? router.push("./main") : router.push("./login"))
  }
  return (
    <main className={styles.main} >
      <div className="header px-2">
        <div className="logo"><Image src="/logo2.png" alt="logo" width={36} height={36} />
          <h1>ROLAX</h1>
        </div>
        <button className="button" onClick={handleLogin} style={{ height: 36, width: 160 }}><p className={manrope.className} style={{ fontSize: 14, fontWeight: 600 }}>Login</p></button>
      </div>
      <section className="relative w-full h-[40rem]">
        <Image
          className="w-full h-full object-cover"
          src="/onBoarding3.png"
          alt="onBoarding"
          width={0}
          height={0}
          objectFit="cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 flex flex-col justify-center items-center gap-6 mx-32">
          <h1 className={["text-white font-bold text-8xl", lexend.className].join(" ")}>
            Manage Your Pharmacy Effortlessly
          </h1>
          <h1 className={["text-white font-normal text-5xl", manrope.className].join(" ")}>
            Streamline your pharmacy operations with cutting-edge tools and features.
          </h1>
          <div className="w-full mt-8 flex justify-end">
            <button className="button" onClick={handleLogin} style={{ height: 36, width: 160 }}>
              <p className={manrope.className} style={{ fontSize: 14, fontWeight: 600 }}>
                Get Started
              </p>
            </button>
          </div>
        </div>
      </section>
      <section>
        <h1 className={["text-5xl text-customPurple font-bold text-center mt-14", lexend.className].join(" ")}> Feature Overview</h1>
        <div className="flex mx-32 my-14" >
          <div className="card w-1/3 ">
            <div className="cardText">
              <div className="flex items-center gap-1">
                <Image src="/icons8-inventory-250.png" width={36} height={36} alt="inventory management" />
                <h2 className={[" font-normal text-xl", lexend.className].join(" ")}>
                  Inventory Management
                </h2>
              </div>
              <p className={[" font-normal text-sm", manrope.className].join(" ")}>
                Monitor stock levels, and streamline recording processes for efficient inventory control.
              </p>
            </div>
            <Image src="/Frame3.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
          <div className="card w-1/3">
            <div className="cardText">
              <div className="flex items-center gap-1">
                <Image src="/icons8-sales-64.png" width={36} height={36} alt="Sales Management" />
                <h2 className={[" font-normal text-xl", lexend.className].join(" ")}>
                  Sales Management
                </h2>
              </div>
              <p className={[" font-normal text-sm", manrope.className].join(" ")}>
                Manage customer orders, save all reciepts and enusre time efficient operations.
              </p>
            </div>
            <Image src="/Frame2.png" width={0} height={0} sizes="100vw" alt="Sales Management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
          <div className="card w-1/3">
            <div className="cardText">
              <h2 className={[" font-normal text-xl", lexend.className].join(" ")}>
                <div className="flex items-center gap-1">
                  <Image src="/icons8-purchase-64.png" width={36} height={36} alt="Sales Management" />
                  <h2 className={[" font-normal text-xl", lexend.className].join(" ")}>
                    Purchase Management
                  </h2>
                </div>
              </h2>
              <p className={[" font-normal text-sm", manrope.className].join(" ")}>
                Streamline purchase orders and supplier management processes.
              </p>
            </div>
            <Image src="/Frame14.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
        </div>
      </section>
      <section className="bg-customPurple text-white">
        <h1 className="pt-14 text-5xl font-bold text-center">
          About us
        </h1>
        <div className="mx-32 flex items-center justify-center py-14">
          <Image src="/capsules.png" width={0} height={0} sizes="100vw" alt="about us" style={{ borderRadius: 6, marginRight: 16, width: "15%" }} />
          <p className={["text-white text-2xl", manrope.className].join(" ")} >
          ROLAX is a comprehensive, cutting-edge pharmacy management system designed to revolutionize the way pharmacies operate. We are committed to enhancing the efficiency, accuracy, and overall performance of pharmacy operations through our innovative suite of tools and features. With years of experience and a deep understanding of the pharmacy industry, we continuously push the boundaries of innovation to meet the ever-evolving needs of modern pharmacies.
          </p>
        </div>
        <div className="flex mx-32 pb-14" >
          <div className="card w-1/2 " style={{ background: "#6D3DED" }}>
            <div className="cardText">
              <div className="flex items-center gap-1">
                <h2 className={[" font-normal text-5xl", lexend.className].join(" ")}>
                  John Mokaya
                </h2>
              </div>
              <p className={[" font-normal text-xl", manrope.className].join(" ")}>
                TELECOMMUNICATIONS student and a software developer .I am passionate about IOT and Software Development.
              </p>
            </div>
            <Image src="/john.png" width={0} height={0} sizes="100vw" alt="inventory management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
          <div className="card w-1/2 " style={{ background: "#6D3DED" }}>
            <div className="cardText">
              <div className="flex items-center gap-1">
                <h2 className={[" font-normal text-5xl", lexend.className].join(" ")}>
                  Mohamed Alaga
                </h2>
              </div>
              <p className={[" font-normal text-xl", manrope.className].join(" ")}>
              A Full-Stack Software Engineer with expertise in Mobile Apps, Web Development, Automation, and creating innovative, scalable solutions
              </p>
            </div>
            <Image src="/alaga.jpeg" width={0} height={0} sizes="100vw" alt="Sales Management" style={{ borderRadius: 6, height: "100%", width: "50%" }} />
          </div>
        </div>
      </section>
      <section className={styles.contactusSection}>
        <div className=" flex flex-col items-center justify-between gap-3 h-[18rem] w-[32rem] text-center">
          <h1 className={["text-5xl text-customPurple font-bold", lexend.className].join(" ")}>
            Need to talk with us?
          </h1>
          <p className={["text-lg ", manrope.className].join(" ")}>
            Get in touch with our team for any queries or support. We're here to help you!
          </p>
          <a className="button my-8" href="https://github.com/MohamedAlaga/ALX_phase_one_project" style={{ width: 132, height: 52 }}>
            <p className={manrope.className} style={{ fontSize: 14, fontWeight: 600, color: "white" }}>
              Contact us
            </p>
          </a>
        </div>
      </section>
      <footer className="bg-customPurple text-white">
        <div className="flex justify-center items-center gap-3 h-10">
          <p className={["text-sm", manrope.className].join(" ")}>
            © 2024 ROLAX. All rights reserved
          </p>
          <p className={["text-sm", manrope.className].join(" ")}>
            Terms of Service
          </p>
          <p className={["text-sm", manrope.className].join(" ")}>
            Privacy Policy
          </p>
        </div>
      </footer>
    </main>
  );
}
