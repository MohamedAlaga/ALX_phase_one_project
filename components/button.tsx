import Image from "next/image";

type ButtonProps = {
  type: 'button' | 'submit';
  title: string;
  icon?: string;
  variant: 'primary' | 'secondary' | 'google' | 'apple';
  full?: boolean;
  style: any
}

const Button = ({ type, title, icon, variant, full }: ButtonProps) => {
  let baseClasses = "flexCenter gap-3 rounded-full border text-sm font-bold px-6 py-2";
  let variantClasses = "";

  switch(variant) {
    case 'primary':
      variantClasses = "bg-purple-600 text-white";
      break;
    case 'secondary':
      variantClasses = "bg-transparent border-gray-300 text-gray-600";
      break;
    case 'google':
      variantClasses = "bg-white border-gray-300 text-gray-600";
      break;
    case 'apple':
      variantClasses = "bg-white border-gray-300 text-gray-600";
      break;
    default:
      variantClasses = "bg-gray-200 text-gray-600";
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses} ${full && 'w-full'}`}
      type={type}
    >
      {icon && <Image src={icon} alt={title} width={24} height={24} />}
      <span className="whitespace-nowrap">{title}</span>
    </button>
  )
}

export default Button;
