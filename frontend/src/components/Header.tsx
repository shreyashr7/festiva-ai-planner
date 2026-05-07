import { PartyPopper, Wifi, WifiOff } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface HeaderProps {
  apiStatus: "connected" | "offline" | "checking";
}

export default function Header({ apiStatus }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-border/60 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-[1440px] items-center justify-between px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 shadow-md">
            <PartyPopper className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">
              Festiva{" "}
              <span className="bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
                AI
              </span>
            </h1>
            <p className="text-[11px] text-muted-foreground -mt-0.5">Premium Event Planning</p>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          <Badge
            variant={
              apiStatus === "connected" ? "success" : apiStatus === "offline" ? "danger" : "secondary"
            }
            className="gap-1.5"
          >
            {apiStatus === "connected" ? (
              <Wifi className="h-3 w-3" />
            ) : (
              <WifiOff className="h-3 w-3" />
            )}
            {apiStatus === "connected"
              ? "API Connected"
              : apiStatus === "offline"
                ? "API Offline"
                : "Checking…"}
          </Badge>
        </div>
      </div>
    </header>
  );
}
